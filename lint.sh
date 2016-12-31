#!/bin/sh
bundle exec rubocop -Daf fuubar
bundle exec haml-lint source
bundle exec scss-lint source