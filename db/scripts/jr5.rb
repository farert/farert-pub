#! ruby -Ks


=begin sample data

˜HüˆêˆÓ‰º
JR–kŠC“¹	”ŸŠÙ–{ü	0		”ŸŠÙ‰w	‚Í‚±‚¾‚Ä	 
JR–kŠC“¹	”ŸŠÙ–{ü	3.4		ŒÜ—ÅŠs‰w	‚²‚è‚å‚¤‚©‚­	¡]·ü
JR–kŠC“¹	”ŸŠÙ–{ü	8.3		‹j[‰w	‚«‚«‚å‚¤	 
 :

–kŠC“¹	JR–kŠC“¹	”ŸŠÙü	”ŸŠÙ‰w	‚Í‚±‚¾‚Ä	0	0	 	

‰w–¼‚ÅA‰w‚Æ‚¢‚¤•¶š‚ª¬‚¶‚Á‚Ä‚¢‚é‰w
d•¡‰w–¼

‚ğ’Šo

=end

if ARGV[0] 
  fn = ARGV[0] 
else
  fn = 'jr.txt'
end
ln = 0
h_eki = Hash.new(0)
r1 = Regexp::new('‰w.*‰w')
r2 = Regexp::new('.+‰w\Z')
e1 = Array::new
e2 = Array::new
branch = Hash.new("")
IO.foreach(fn) do |lin|
  ln += 1
  linitems = lin.split(/\t/)
  eki = linitems[3]		# ‰w
  h_eki[eki] += 1
  train_lines = Array.new
  train_lines << linitems[2]    # ˜Hü 
	if linitems[7].strip != ""
  	train_lines.concat linitems[7].split(/\//)
  end
  train_lines.map! {|m| m.strip }
	train_lines.compact!     				   # nil ‚ğ”z—ñ‚©‚çæ‚èo‚·
	train_lines.reject! {|m| m == ""}  # ‹ó•¶š‚à”z—ñ‚©‚çœ‹
  train_lines.sort!									 # ˜HüA•ªŠò˜HüŒQ‚Ì”z—ñƒ\[ƒg
  if branch[eki] != ""
    branch[eki] += ","
  end
  branch[eki] += train_lines.join("|")   # Še‰w–ˆ‚É˜HüA•ªŠò˜HüŒQ‚ğ|‹æØ‚è‚Ì•¶š—ñ‚Å•Û

  if r1.match(eki)   # ‰w‚ğŠÜ‚Ş‰w
	  e1 << sprintf("%s(%d): %s", fn, ln, eki)
  end
  unless r2.match(eki) # ‰w‚ÅI‚í‚Á‚Ä‚¢‚È‚¢‰w
	  e2 << sprintf("%s(%d): %s", fn, ln, eki)
  end
end    
puts("–––‰w‚Æ‚¢‚¤•¶š‚ª•¡”–––")
e1.each do |e|
   puts(e)
end
#puts("–––‰w‚Æ‚¢‚¤•¶š‚ÅI‚í‚Á‚Ä‚¢‚È‚¢–––")
#e2.each do |e|
#   puts(e)
#end
puts("–––d•¡‰w–¼ or •ªŠò‰w(Š‘®˜Hü‚ª•¡”)–––")
# ]·ü|”ŸŠÙü,]·ü|”ŸŠÙü
# ”ŸŠÙü

# h_keys  Še‰w“oê‰ñ”‚ğ•Û
# branch  Še‰wŠ‘®˜Hü‚ğ•Û
#
h_eki.keys.each do |e|				# Še‰w–ˆ
  bra = branch[e].split(",")   # ‰w‚ª2‰ñˆÈã‚ ‚éê‡, bra‚ÉŒÂ”•ª‚ÌŠ‘®˜Hü‚Ì”z—ñ‚ª“ü‚é
  bra.map! {|r| r.split("|") }
  if 1 < h_eki[e] # •ªŠò‰w or 2“xˆÈã“oê‚µ‚½‰w e
    if bra.length != h_eki[e]
      puts "!!!!!!!!!bug!!!!! #{e}:#{bra.length}"
    end
    puts(e + "(#{h_eki[e]})")   # ‰w–¼(“oê”)
		other_station_lines = nil
		n_eki = 0
    bra.each do |station_lines|		# “¯–¼‰w–ˆ
      n_eki += 1
			unless other_station_lines
				other_station_lines = station_lines
				if station_lines.length <= 0
					puts "!!!!!bug!!!!!"
				elsif station_lines.length  == 1
					puts "  #{e}‰w#{n_eki}/#{bra.length}: ‰w•¡”‚È‚Ì‚É•ªŠò‰w‚È‚µ(“¯–¼‰w)"
				elsif station_lines.length != h_eki[e]
					puts "  #{e}‰w#{n_eki}/#{bra.length}: •ªŠò˜Hü”‚Ì‘Šˆá #{station_lines.length}, #{h_eki[e]}: #{station_lines.join('/')}"
				end
			end
			if other_station_lines != station_lines and station_lines.length != 1
				puts "  #{e}‰w#{n_eki}/#{bra.length}: •ªŠò˜Hü•s‘«: #{other_station_lines.join('/')}, #{station_lines.join('/')}"
			elsif station_lines.length == 1
				puts "               #{station_lines.join('/')}"
			end
    end
  else # ‰w1ŒÂ(•ªŠò‚È‚µ)
	  if 1 < bra[0].length
      puts "‰wˆêŒÂ‚È‚Ì‚É•ªŠò‰wH #{e}:#{bra.length}->#{bra[0]}"
	  end
  end
end


