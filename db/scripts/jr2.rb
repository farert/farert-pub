#! ruby -Ks


=begin sample data
0.0
3.4
8.3
10.4
13.8
17.9
21.2
27.0
28.0
31.7
36.5
40.1
44.2
49.5
52.2
56.1
60.0
 :
 :
 :
‰c‹ÆƒLƒ‚ÌƒCƒŠ[ƒKƒ‹ƒtƒH[ƒ}ƒbƒg‚ÌŒŸo

–kŠC“¹	JR–kŠC“¹	”ŸŠÙü	”ŸŠÙ‰w	‚Í‚±‚¾‚Ä	0	0	 	

=end

if ARGV[0] 
  fn ARGV[0] 
else
  fn = 'jr.txt'
end
ln = 0
err = 0
re1 = Regexp::new(/\d+\.\d+/)
re2 = Regexp::new(/\d+/)
rosen = ''
IO.foreach(fn) do |lin|
	ln += 1
	sen = lin.split(/\t/)[2]
	if sen != rosen
	  skm0 = 0.to_f
	  ckm0 = 0.to_f
	  rosen = sen
	end
	skm, ckm = lin.split(/\t/)[5, 2]
	unless rd1 = re1.match(skm)
	  rd1 = re2.match(skm)
	end 
	unless rd2 = re1.match(ckm)
	  rd2 = re2.match(ckm)
	end 
	if !rd1 || (rd1[0] != skm) || !rd2 || (rd2[0] != ckm)
##		if rd1 && (rd1[0] != skm)
##		  puts rd1[0] + "@" + skm + "#{fn}(#{ln}): " + lin
##	elsif rd2 && (rd2[0] != ckm)
##		  puts rd2[0] + "@" + ckm + "#{fn}(#{ln}): " + lin
##		else
		if rd1 && (rd1[0].to_f != skm.to_f)
			puts "#{fn}(#{ln}): " + lin.chomp() + "skm" + rd1[0] + "@" + skm
		elsif rd2 && (rd2[0].to_f != ckm.to_f)
			puts "#{fn}(#{ln}): " + lin.chomp() + "ckm" + rd2[0] + "--" + ckm
    elsif !rd1
			puts "#{fn}(#{ln}): " + lin.chomp() + "skm null"
		elsif !rd2
			puts "#{fn}(#{ln}): " + lin.chomp() + "ckm null"
	  else
		end
		err += 1
	else
		if skm.to_f < skm0.to_f || (skm0 == 0 && skm.to_f != 0)
		  puts "#{fn}(#{ln})! " + lin.chomp() + "skm0" + "skm=#{skm},skm0=#{skm0}"
		elsif ckm.to_f < ckm0.to_f || (ckm0 == 0 && ckm.to_f != 0)
		  puts "#{fn}(#{ln})# " + lin.chomp() + "ckm0"
		end
		skm0 = skm.to_f
		ckm0 = ckm.to_f
  end
end
puts "err=#{err} line / #{ln}"

