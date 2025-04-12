export const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold mb-4">404 - Page Not Found</h1>
      <p className="text-lg text-center max-w-2xl">
        Sorry, the page you are looking for does not exist. You can go back to
        the homepage or check out our other pages.
      </p>
    </div>
  );
}
export default NotFound;