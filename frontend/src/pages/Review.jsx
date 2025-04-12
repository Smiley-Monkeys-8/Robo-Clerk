export const Review = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-blue-zodiac text-white">
      <h1 className="text-4xl font-bold mb-4">Review</h1>
      <p className="text-lg mb-8">Your feedback is important to us!</p>
      <form className="flex flex-col gap-4">
        <textarea
          className="p-4 rounded-lg border border-gray-300"
          rows="5"
          placeholder="Write your review here..."
        ></textarea>
        <button
          type="submit"
          className="bg-white text-blue-zodiac py-2 px-4 rounded-lg font-bold hover:bg-gray-200 transition duration-300"
        >
          Submit Review
        </button>
      </form>
    </div>
  );
}
export default Review;