prev_score = -1
incr = 500000


function gameActive()
	game_status = memory.readbyte(0x0048)
	pause_status = memory.readbyte(0x00A7)
	if (game_status == 10) or (game_status == 00) or (pause_status == 7) then
		return false
	else
		return true
	end
end


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
		displayScore()
	else
		prev_score = -1
		incr = 500000
	end

	-- advance the game 5 frames
	for i = 0, 1 do
		emu.frameadvance()
	end
end