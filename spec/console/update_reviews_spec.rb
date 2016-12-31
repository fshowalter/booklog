# frozen_string_literal: true
require 'spec_helper'
require 'support/io_helper'

describe Movielog::Console::UpdateReviews do
  before(:each) do
    expect(Movielog).to receive(:reviews).and_return({})
  end

  it 'calls Movielog::Db::UpdateMostReviewedTables' do
    expect(Movielog::Db::UpdateMostReviewedTables).to receive(:call).and_return(true)

    Movielog::Console::UpdateReviews.call
  end
end
