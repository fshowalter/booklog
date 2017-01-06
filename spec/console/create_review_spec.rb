# frozen_string_literal: true
require 'spec_helper'
require 'support/io_helper'

describe Booklog::Console::CreateReview do
  let(:books) do
    {
      'the-shining-by-stephen-king' => OpenStruct.new(
        id: 'the-shining-by-stephen-king',
        title: 'The Shining',
        authors: [
          OpenStruct.new(name: 'Stephen King')
        ]
      )
    }
  end

  before(:each) do
    IOHelper.clear
    allow(Booklog).to receive(:next_review_number).and_return(9999)
    allow(File).to receive(:open).and_call_original
    allow(File).to receive(:open).with(Booklog.reviews_path + '/9999-the-shining-by-stephen-king.md', 'w')
  end

  it 'creates review' do
    expect(Booklog).to receive(:books).and_return(books)
    expect(Booklog::Console::CreateReview).to(receive(:puts))

    IOHelper.type_input('the shining')
    IOHelper.type_input("\r")

    review = Booklog::Console::CreateReview.call
    expect(review.book_id).to eq 'the-shining-by-stephen-king'
    expect(review.sequence).to eq 9999
  end
end
