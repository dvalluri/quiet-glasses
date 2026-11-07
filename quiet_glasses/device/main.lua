-- ASCII protocol: A|generation, T|generation|sequence|text, D|generation.
-- Receive callbacks execute serially in the Halo runtime.
local generation = 0
local active = false
local sequence = 0
-- Physical BLE sends can fail during disconnect; clearing must still succeed.
local function notify(message)
    if frame.bluetooth.is_connected() then
        pcall(frame.bluetooth.send, message)
    end
end
local function blank()
    frame.display.clear(0x000000)
    frame.display.show()
end
local function dismiss()
    active = false
    blank()
    notify('DISMISSED|' .. generation)
end
frame.display.set_font(0, 8, 1)
frame.display.set_pan(0, 0)
blank()
-- Halo's show() is a no-op; framebuffer writes do not wake the panel.
frame.display.power_save(false)
frame.button.single(dismiss)
frame.button.long(dismiss)
frame.bluetooth.receive_callback(function(data)
    local kind, g, rest = data:match('^(%u)|(%d+)|?(.*)$')
    g = tonumber(g)
    if not g then return end
    if kind == 'A' and g > generation then
        generation = g
        sequence = 0
        active = true
        blank()
        notify('ACTIVE|' .. g)
    elseif kind == 'D' and g >= generation then
        generation = g
        dismiss()
    elseif kind == 'T' and active and g == generation then
        local seq, text = rest:match('^(%d+)|(.*)$')
        seq = tonumber(seq)
        if not seq or seq <= sequence or not text or #text > 174 then return end
        sequence = seq
        blank()
        local row = 0
        for line in (text .. '\n'):gmatch('(.-)\n') do
            if row >= 6 then break end
            frame.display.text(line, 13, 77 + row * 16, 0xFFFFFF)
            row = row + 1
        end
        frame.display.show()
        notify('DRAWN|' .. g .. '|' .. seq)
    end
end)
notify('READY')
while true do
    if not frame.bluetooth.is_connected() then active = false; blank() end
    frame.sleep(0.005)
end
