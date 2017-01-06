# -*- encoding: utf-8 -*-
$:.push File.expand_path("../lib", __FILE__)

Gem::Specification.new do |s|
  s.name        = "middleman-sitemap"
  s.version     = "0.0.13"
  s.platform    = Gem::Platform::RUBY
  s.authors     = ["Larry Staton Jr."]
  s.email       = ["larry@larrystaton.com"]
  s.homepage    = "https://github.com/statonjr/middleman-sitemap"
  s.summary     = %q{Builds a sitemap.xml for your site}
  s.description = %q{Builds a sitemap.xml for your site}

  s.files         = Dir['**/*.*']
  s.executables   = s.files.grep(%r{^bin/}) { |f| File.basename(f) }
  s.test_files    = s.files.grep(%r{^(test|spec|features)/})
  s.require_paths = ["lib"]

  # The version of middleman-core your extension depends on
  s.add_runtime_dependency("middleman-core", [">= 3.2.2"])

end
