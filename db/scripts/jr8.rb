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
  fn ARGV[0] 
else
  fn = 'jr.txt'
end
ln = 0
h_eki = Hash.new(0)
r1 = Regexp::new('‰w.*‰w')
r2 = Regexp::new('.+‰w\Z')
e1 = Array::new
e2 = Array::new
branch = Hash.new([])
IO.foreach(fn) do |lin|
  ln += 1
  linitems = lin.split(/\t/)
  eki = linitems[3]		# ‰w
  h_eki[eki] += 1
  branches = Array.new
  branches << linitems[2]
	if linitems[7]
  	branches.concat linitems[7].split(/\//)
  end
  branches.map! {|m| m.strip }
  branch[eki] << branches.join(",")
  if r1.match(eki)
	  e1 << sprintf("%s(%d): %s", fn, ln, eki)
  end
  unless r2.match(eki)
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
puts("–––d•¡‰w–¼–––")
h_eki.keys.each do |e|
  if 1 < h_eki[e]
    s = ""
    d = []
    1.upto(branch[e].length - 1) do |i|
      if branch[e][0] != branch[e][i]
puts e + "===" + branch[e][i] + "/"
        d << branch[e][i]
      else
      puts "ppppppppppppppppppppppppppp"
      end
    end
    if 0 < d.length
      s = branch[e][0]
      d.each do |de|
        if de
         s += "=>"
         s += de
        else
        puts "‚»‚ñ‚È‚Ì‚ ‚é‚©‚¢"
        end
      end
    else
      s = ""
    end
    puts(e + "(#{h_eki[e]})\t#{s}")
exit
  end
end


