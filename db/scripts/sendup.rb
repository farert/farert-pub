#! ruby -Ks

if ARGV[0] 
  fn ARGV[0] 
else
  fn = 'jr.txt'
end

ss = '‰w'
ss = 'ü'
ln = 0
IO.foreach(fn) do |lin|
  ln += 1
	#print lin
	cs = lin.split(/\s+/)[0..5].join("\t")
	s = cs.sub(ss, '!')
	if s.include?(ss)
	  puts "#{fn}(#{ln}): #{lin}"
	end
end

