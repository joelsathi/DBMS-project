import { Admin, Resource, ListGuesser, CustomRoutes, convertLegacyDataProvider } from "react-admin";
import jsonServerProvider from "ra-data-json-server";
import { Route } from "react-router-dom";

import dataProvider from "./api/dataProvider";

import { SingleProduct } from "./container";

// import { Testing } from "./container";

const App = () => (
  <Admin dataProvider={dataProvider}>
    <Resource name="posts" list={ListGuesser} />
    <Resource name="comments" list={ListGuesser} />
  <CustomRoutes>
    <Route path="/Checkout" element={<SingleProduct/>}/>
    {/* <Route path="/testingDP" element={<Testing/>}/> */}
  </CustomRoutes>
  </Admin>
);

export default App;
