import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Product } from '../../components/product-card';
import publicAxios from '../../utils/public-axios';

export interface ProductSliceState {
  product: Product | null;
  loading: boolean;
  error: null | object;
  product_variants: string[];
}

const initialState: ProductSliceState = {
  product: null,
  loading: false,
  error: null, 
  product_variants: [],
};

export const getProductById = createAsyncThunk(
  'products/details',
  async (u: any) => {
    if (u.id) {
      try {
        const productVariantsResponse = await publicAxios.get(`/product/variants/${u.id}`);
        console.log('IN PRODUCT DETAILS, productVariantsResponse.data', productVariantsResponse.data);
        // const productVariantResponse = await publicAxios.get(`/product/variant_filtered/search?sku=${u.sku}`);
        // console.log('IN PRODUCT DETAILS, productVariantResponse.data', productVariantResponse.data);

        // modify
        if(u.sku === undefined) { u.sku = '' }
        const productResponse = await publicAxios.get(`/product/product_variant_filtered/search?id=${u.id}&sku=${u.sku}`);
        // const productResponse = await publicAxios.get(`/product/product_variant_filtered/search?id=${u.id}&sku=ABCD1235`);

        console.log('IN PRODUCT DETAILS, productResponse.data', productResponse.data[0]);
        
        

        // const productOptionsResponse = await publicAxios.get(`/product/options/${u.id}`);
        // console.log('IN PRODUCT DETAILS, productOptionsResponse.data', productOptionsResponse.data);


      return {
        product: productResponse.data[0],
        productVariantsResponse: productVariantsResponse.data.data,
        // variant: variant,
        // variant_options: productOptionsResponse.data.data,
      };
    } catch (error) { }
  }
  }
);

export const productDetailsSlice = createSlice({
  name: 'product-detail',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(getProductById.pending, (state) => {
      // Add user to the state array
      state.loading = true;
    });
    builder.addCase(getProductById.fulfilled, (state, action) => {
      state.loading = false;
      state.product = action.payload?.product;
      state.product_variants = action.payload?.productVariantsResponse;
    });
    builder.addCase(
      getProductById.rejected,
      (state, action: PayloadAction<any>) => {
        state.loading = false;
        state.error = action.payload;
      }
    );
  },
});

// Action creators are generated for each case reducer function

export default productDetailsSlice;
