#! ruby -Ks


=begin sample data

˜HüˆêˆÓ‰º
–kŠC“¹	JR–kŠC“¹	”ŸŠÙü	”ŸŠÙ‰w	‚Í‚±‚¾‚Ä	0	0	 	
 :


˜Hüˆê——(d•¡‚Í*ƒ}[ƒN‚Æd•¡”)
ü‚ÅI‚í‚Á‚Ä‚È‚¢ü‹æ
xüˆê——
(xxx`xxx)‚É‚È‚Á‚Ä‚¢‚È‚¢xü

‚ğ’Šo

=end

if ARGV[0] 
  fn ARGV[0] 
else
  fn = 'jr.txt'
end

rosens = []
rosen = ''

IO.foreach(fn) do |lin|
  item = lin.split(/\t/)
  if rosen != item[2]
    rosens << item[2]
    rosen = item[2]
	end
end


h = Hash.new(0)
rosens.each do |r|
  h[r] += 1
  if 1 < h[r]
    puts('*' + r + "(#{h[r]})")
  else
    puts(r)
  end
end
puts("‘S#{h.length}˜Hü")

puts("******* xüˆê—— ********")
sisen = []
r = Regexp::new('.+\(.+`.+\)\Z')
h.keys.each do |k|
  if r.match(k)
    puts("#{k}")
    sisen << k
  end
end


puts("******* ü‚Å‚È‚¢ ********")
h.keys.each do |k|
  if k[-1] != 'ü'
    fsisen = 0
    sisen.each do |ss|
      if ss == k 
        fsisen = 1
      end
    end
    if fsisen != 1
      puts("#{k}")
    end
  end
end


