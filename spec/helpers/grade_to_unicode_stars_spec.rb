# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_template_context'

describe Movielog::Helpers do
  let(:context) { stub_template_context }
  describe '#grade_to_unicode_stars' do
    ('A'..'D').each do |letter|
      ['+', '', '-'].each do |modifier|
        grade = "#{letter}#{modifier}"
        context "when grade is #{grade}" do
          it 'returns an unicode string' do
            unicode = context.grade_to_unicode_stars(grade: grade)
            expect(unicode).not_to be_blank
          end
        end
      end
    end

    context 'when grade is F' do
      it 'returns an unicode string' do
        unicode = context.grade_to_unicode_stars(grade: 'F')
        expect(unicode).not_to be_blank
      end
    end

    context 'when grade is blank' do
      it 'returns an empty string' do
        expect(context.grade_to_unicode_stars(grade: nil)).to eq('')
      end
    end
  end
end
