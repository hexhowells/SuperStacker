local tcplib = require("lualibs.socket")


function buttonPressed(controller)
	for k,v in pairs(controller) do
		if v then 
			return true 
		end
	end
	return false
end


function getScreen(screen)
	local screen_arr = ''
	for i = 0, 199 do
		block = nil
		if screen[i] ~= 239 then
			block = 1
		else
			block = 0
		end
		screen_arr = screen_arr .. ',' .. block
	end
	return screen_arr:sub(2)
end


function pieceArray(piece)
	local piece_arr = ''
	for k,v in pairs(piece) do
		piece_arr = piece_arr .. ',' .. v
	end
	return piece_arr:sub(2)
end


function gameActive()
	game_status = memory.readbyte(0x0048)
	pause_status = memory.readbyte(0x00A7)
	if (game_status == 10) or (game_status == 00) or (pause_status == 7) then
		return false
	else
		return true
	end
end


function gameOver()
	game_status = memory.readbyte(0x0048)
	if (game_status == 10) then
		return '1'
	else
		return '0'
	end
end


function getReward()
	lines_cleared = memory.readbyte(0x0056)
	return lines_cleared
end


function getControllerMap(input_vec)
	defaultInput = {["A"] = false,
                    ["B"] = false,
                    ["Down"] = false,
                    ["Left"] = false,
                    ["Right"] = false,
                    ["Up"] = false}
    
    if input_vec:sub(1,1) == '1' then
    	defaultInput["Up"] = true
    elseif input_vec:sub(3,3) == '1' then
    	defaultInput["A"] = true
    elseif input_vec:sub(4,4) == '1' then
    	defaultInput["Left"] = true
   	elseif input_vec:sub(5,5) == '1' then
    	defaultInput["Down"] = true
   	elseif input_vec:sub(9,9) == '1' then
    	defaultInput["B"] = true
    elseif input_vec:sub(10,10) == '1' then
    	defaultInput["Right"] = true
    end

    return defaultInput
end


function getDropped()
	d = 0
	d = d + tonumber( string.format("%x", memory.read_s16_le(0x03F0)) )
	d = d + tonumber( string.format("%x", memory.read_s16_le(0x03F2)) )
	d = d + tonumber( string.format("%x", memory.read_s16_le(0x03F4)) )
	d = d + tonumber( string.format("%x", memory.read_s16_le(0x03F6)) )
	d = d + tonumber( string.format("%x", memory.read_s16_le(0x03F8)) )
	d = d + tonumber( string.format("%x", memory.read_s16_le(0x03FA)) )
	d = d + tonumber( string.format("%x", memory.read_s16_le(0x03FC)) )

	return d
end


prev_score = -1
incr = 500000
function getScore()
	score = string.format("%x", memory.read_s24_le(0x0053))
	score = string.gsub(score, "a", "10")
	score = string.gsub(score, "b", "11")
	score = string.gsub(score, "c", "12")
	score = string.gsub(score, "d", "13")
	score = string.gsub(score, "e", "14")
	score = string.gsub(score, "f", "")

	score_num = tonumber(score)
	if (score_num < prev_score) then
		score_num = score_num + incr
		incr = incr + 500000
	end
	prev_score = score_num

	return tostring(score_num)
end


function displayScore()
	gui.drawBox(188, 75, 243, 90, nil, "black")
	score = getScore()
	gui.drawText(189, 76, score, nil, nil, 10, "Arial")
end


while true do
	if gameActive() then
		-- display accurate score
		displayScore()

		-- connect to the socket
		tcp = tcplib.tcp()
		success = tcp:connect('localhost', 65432)

		-- get the data from the emulator
		screen = memory.readbyterange(0x0400, 200)
		controller = joypad.get()
		piece = memory.readbyterange(0x0040, 3)
		next_piece = memory.readbyte(0x0019)
		reward = getReward()

		-- send data to the server
		frame_data = getScreen(screen) .. '\n' 
		.. pieceArray(piece) .. '\n' 
		.. next_piece .. '\n' 
		.. reward .. '\n' 
		.. gameOver() .. '\n'
		.. getDropped()

		tcp:send(frame_data)

		-- recieve controller input array from server
		_, status, data = tcp:receive('*l')
		--console.log(data)

		-- convert input vector to an input map and invoke new control
		input_map = getControllerMap(data)
		joypad.set(input_map, 1)

	else
		console.clear()
		console.log("score: ", getScore())
		gui.clearGraphics()

		joypad.set({Start=true}, 1)

		-- reset score calculation variables
		prev_score = -1
		incr = 500000
	end
	
	-- advance the game 5 frames
	for i = 0, 1 do
		emu.frameadvance()
	end
end