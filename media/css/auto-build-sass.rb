#!/usr/bin/env ruby

CHECK_PERIOD = 5      # in seconds

def find_sass_files
  return Dir["*.sass"]
end

def css_name(fname)
  return File.basename(fname,'.sass') + '.css'
end

def is_dirty?(fname)
  sass_mtime = File.stat(fname).mtime
  output = css_name(fname)
  return true if !(FileTest.exists? output)
  css_mtime = File.stat(output).mtime
  return (css_mtime < sass_mtime)
end

def build(fname)
  output = css_name(fname)
  puts "Building #{fname}..."
  system("sass #{fname} #{output}")
  puts "done."
end

sass_files = find_sass_files
begin
  sass_files.each do |fname|
    if is_dirty?(fname)
      build(fname)
    end
  end
end while(true)
