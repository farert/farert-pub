#! ruby -Ks


=begin sample data

˜HüˆêˆÓ‰º
ken	JR–kŠC“¹	”ŸŠÙ–{ü	0		”ŸŠÙ‰w	‚Í‚±‚¾‚Ä	 
len JR–kŠC“¹	”ŸŠÙ–{ü	3.4		ŒÜ—ÅŠs‰w	‚²‚è‚å‚¤‚©‚­	¡]·ü
len JR–kŠC“¹	”ŸŠÙ–{ü	8.3		‹j[‰w	‚«‚«‚å‚¤	 
 :

jr6.rb		‰w–¼‚ÅA‰w‚Å‚¨‚í‚Á‚Ä‚¢‚È‚¢‰w(‘SsƒXƒLƒƒƒ“)B

jr.txt
‚ğ’Šo

=end

if ARGV[0] 
  fn ARGV[0] 
else
  fn = 'jr.txt'
end
ln = 0
r2 = Regexp::new('.+‰w\Z')
IO.foreach(fn) do |lin|
  ln += 1
  eki = lin.split(/\t/)[3]		# ‰w
  unless r2.match(eki)
	  puts sprintf("%s(%d): %s", fn, ln, eki)
  end
end

