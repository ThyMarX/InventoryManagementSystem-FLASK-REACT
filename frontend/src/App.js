// This is where we choose which "page" to show on the app.
// For now we'll try and keep all the features of the system on just one page, but in the future there might be more.

import Frontpage from "./pages/Frontpage";

function App() {
  return (
    <div className="flex justify-center h-screen ">

      <Frontpage />

    </div>

  );
}

export default App;
