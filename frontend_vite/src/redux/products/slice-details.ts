import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Product } from '../../components/product-card';
import publicAxios from '../../utils/public-axios';

export interface ProductSliceState {
  product: Product | null;
  loading: boolean;
  error: null | object;
  variant_options: string[];
  variant: string[];
  product_variants: string[];
}

const initialState: ProductSliceState = {
  product: null,
  loading: false,
  error: null,
  variant_options: [],
  variant: [], 
  product_variants: [],
};

export const getProductById = createAsyncThunk(
  'products/details',
  async (u: any) => {
    if (u.id) {
      try {
        const productResponse = await publicAxios.get(`/product/product/${u.id}`);
        console.log('IN PRODUCT DETAILS, productResponse.data', productResponse.data);
        // if u.id is not null, then get the variant

        const productVariantsResponse = await publicAxios.get(`/product/variants/${u.id}`);
        console.log('IN PRODUCT DETAILS, productVariantsResponse.data', productVariantsResponse.data);
        // const productVariantResponse = await publicAxios.get(`/product/variant_filtered/search?sku=${u.sku}`);
        // console.log('IN PRODUCT DETAILS, productVariantResponse.data', productVariantResponse.data);

        let variant = null;
        if (u.sku && u.sku.length === 8) {
        const productVariantResponse = await publicAxios.get(`/product/variant_filtered/search?sku=${u.sku}`);
        console.log('IN PRODUCT DETAILS, productVariantResponse.data', productVariantResponse.data);
        variant = productVariantResponse.data.data;
        }
        
        

        // const productOptionsResponse = await publicAxios.get(`/product/options/${u.id}`);
        // console.log('IN PRODUCT DETAILS, productOptionsResponse.data', productOptionsResponse.data);


      return {
        product: productResponse.data,
        productVariantsResponse: productVariantsResponse.data.data,
        variant: variant,
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
      state.variant = action.payload?.variant;
      state.product_variants = action.payload?.productVariantsResponse;
      // state.variant_options = action.payload?.variant_options;
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
