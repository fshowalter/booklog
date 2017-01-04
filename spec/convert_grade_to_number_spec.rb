# frozen_string_literal: true
require 'spec_helper'

describe Booklog::ConvertGradeToNumber do
  grades = ('A'..'D').map { |l| ['+', '', '-'].map { |m| "#{l}#{m}" } }.flatten

  best = 17
  map = grades.each_with_object({}) do |grade, object|
    object[grade] = best
    best -= 1
  end

  grades.each do |grade|
    it "returns a numeric value for #{grade}" do
      expect(Booklog::ConvertGradeToNumber.call(grade: grade)).to eq map[grade]
    end
  end

  it 'returns a numeric value for F' do
    expect(Booklog::ConvertGradeToNumber.call(grade: 'F')).to eq 5
  end

  it 'returns nil for nil' do
    expect(Booklog::ConvertGradeToNumber.call(grade: nil)).to eq nil
  end
end
