# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_template_context'

describe Movielog::Helpers do
  let(:context) { stub_template_context }
  describe '#grade_to_svg_stars' do
    ('A'..'D').each do |letter|
      ['+', '', '-'].each do |modifier|
        grade = "#{letter}#{modifier}"
        context "when grade is #{grade}" do
          it 'returns an image tag' do
            tag = context.grade_to_image_tag(grade: grade)
            expect(tag).not_to be_blank
          end
        end
      end
    end

    context 'when grade is F' do
      it 'returns an image tag' do
        tag = context.grade_to_image_tag(grade: 'F')
        expect(tag).not_to be_blank
      end
    end

    context 'when grade is blank' do
      it 'returns an empty string' do
        expect(context.grade_to_image_tag(grade: nil)).to eq('')
      end
    end

    context 'when not development' do
      before(:each) { context.development = false }

      it 'returns a full url' do
        tag = context.grade_to_image_tag(grade: 'F')
        expect(tag).to start_with('https://www.franksmovielog.com/')
      end
    end
  end
end
