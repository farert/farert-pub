#! ruby -Ks

if ARGV[0] 
  fn ARGV[0] 
else
  fn = 'jr.txt'
end

ss = 'ü'
ss = '‰w'
ln = 0
IO.foreach(fn) do |lin|
  ln += 1
	s = lin.sub(ss, '!')
	if s.include?(ss)
	  puts "#{fn}(#{ln}): #{lin}"
	end
end

# •Ÿ‰–ü‚Ì‰w‰Æ‰w‚Ì‚İ
