import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import toast from 'react-hot-toast';
import { Product } from '../../components/product-card';
import { setError } from '../../utils/error';
import publicAxios from '../../utils/public-axios';

export interface ProductSliceState {
  products: Product[];
  loading: boolean;
  error: null | object;
  pages: number;
  page: number;
  categories: string[];
  subCategories: string[];
  brands: string[];
  total: number;
}

const products: Product[] | [] = [];

const initialState: ProductSliceState = {
  products: products,
  loading: false,
  error: null,
  categories: [],
  subCategories: [],
  brands: [],
  page: 1,
  pages: 1,
  total: 1,
};


export const getFilterProducts2 = createAsyncThunk(
  'products/filter',
  async (u: any) => {
    try {
      console.log('IN SEARCH LIST##############, u', u);
      const productResponse = await publicAxios.get(`/reports/quarterly_sales_report/search?year=2022-01-16`);
      console.log('IN SEARCH LIST, productResponse.data', productResponse.data);


      // console.log('END ###################');

      return {
        products: productResponse.data.data,


     
      };
    } catch (error: any) {
      const message = setError(error);
      toast.error(message);
    }
  }
);





export const productFilterSlice = createSlice({
  name: 'products-filter',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(getFilterProducts2.pending, (state) => {
      state.loading = true;
    });
    builder.addCase(getFilterProducts2.fulfilled, (state, action) => {
      state.loading = false;
      state.page = 1;
      state.pages = 1;
      state.brands = [];
      state.total = 1;

      state.products = action.payload?.products;
    });
    builder.addCase(getFilterProducts2.rejected, (state) => {
      state.loading = false;
    });
  },
});

export default productFilterSlice;
