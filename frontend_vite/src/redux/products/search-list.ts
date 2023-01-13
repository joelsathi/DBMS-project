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


export const getFilterProducts = createAsyncThunk(
  'products/filter',
  async (u: any) => {
    try {
      console.log('IN SEARCH LIST##############, u', u);
      const productResponse = await publicAxios.get(`/product/product_filtered/search?category=${u.c}&subCategory=${u.sc}&query=${u.q}`);
      const categoriesResponse = await publicAxios.get(`/product/supercategory`);
      //filter based on super category
      const subCategoriesResponse = await publicAxios.get(`/product/subcategory_filtered/search?category=${u.c}`);
      console.log('IN SEARCH LIST, productResponse.data', productResponse.data);
      console.log('IN SEARCH LIST, categoriesResponse.data', categoriesResponse.data);
      console.log('IN SEARCH LIST, subCategoriesResponse.data', subCategoriesResponse.data);

      // console.log('END ###################');

      return {
        products: productResponse.data.data,
        categories: categoriesResponse.data.data,
        subCategories: subCategoriesResponse.data.data,

     
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
    builder.addCase(getFilterProducts.pending, (state) => {
      state.loading = true;
    });
    builder.addCase(getFilterProducts.fulfilled, (state, action) => {
      state.loading = false;
      state.page = 1;
      state.pages = 1;
      state.brands = [];
      state.total = 1;

      state.categories = action.payload?.categories;
      console.log('IN SEARCH LIST, action.payload?.categories', action.payload?.categories);
      state.subCategories = action.payload?.subCategories;
      state.products = action.payload?.products;
    });
    builder.addCase(getFilterProducts.rejected, (state) => {
      state.loading = false;
    });
  },
});

export default productFilterSlice;
