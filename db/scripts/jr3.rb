#! ruby -Ks


=begin sample data

˜HüˆêˆÓ‰º
–kŠC“¹	JR–kŠC“¹	”ŸŠÙü	”ŸŠÙ‰w	‚Í‚±‚¾‚Ä	0	0	 	

JR–kŠC“¹	”ŸŠÙ–{ü	0		”ŸŠÙ‰w	‚Í‚±‚¾‚Ä	 
JR–kŠC“¹	”ŸŠÙ–{ü	3.4		ŒÜ—ÅŠs‰w	‚²‚è‚å‚¤‚©‚­	¡]·ü
JR–kŠC“¹	”ŸŠÙ–{ü	8.3		‹j[‰w	‚«‚«‚å‚¤	 
 :


Å‰‚Ì‰c‹ÆƒLƒ‚ª0km‚Å‚È‚¢‚à‚Ì
‰c‹ÆƒLƒ‚ªŒã‘Ş‚µ‚Ä‚¢‚é‚à‚Ì
‚ğ’Šo‚·‚é

=end

if ARGV[0] 
  fn ARGV[0] 
else
  fn = 'jr.txt'
end

re = Regexp::new('^\d+\.{0,1}\d*\s*\Z')
rosen = ''
ln = 0
km = 0.0
ckm = 0.0
IO.foreach(fn) do |lin|
  ln += 1
  item = lin.split(/\t/)
  if rosen != item[2]
    if (item[5].to_i != 0) || (item[6].to_i != 0)   # Å‰‚Ì‰c‹ÆƒLƒ‚ª0‚Å‚Í‚È‚¢
		  puts "#{fn}(#{ln}): " + lin
    end
      # puts rosen #   + "\t" + km.to_s
    rosen = item[2]
    km = item[5].to_f
    ckm = item[6].to_f
  else
    cur_km = item[5].to_f
    cur_ckm = item[6].to_f
    if cur_km <= km || ((ckm != 0) && (cur_ckm <= ckm))  # ‰c‹ÆƒLƒ‚ªi‚ñ‚Å‚È‚¢‚Ü‚½‚ÍŒã‘Ş
		  puts "#{fn}(#{ln})! " + lin
    end
    km = cur_km
    ckm = cur_ckm
	end
end

