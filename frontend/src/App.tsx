import { Admin, Resource, ListGuesser, CustomRoutes, convertLegacyDataProvider } from "react-admin";
import { Route } from "react-router-dom";

import dataProvider from "./api/dataProvider";

// import { Testing } from "./container";

const App = () => (
  <Admin dataProvider={dataProvider}>
    <Resource name="posts" list={ListGuesser} />
    <Resource name="comments" list={ListGuesser} />
  <CustomRoutes>
    {/* <Route path="/testingDP" element={<Testing/>}/> */}
  </CustomRoutes>
  </Admin>
);

export default App;