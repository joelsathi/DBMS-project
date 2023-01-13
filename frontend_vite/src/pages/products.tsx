import React from 'react';
import { useEffect, useState } from 'react';
import {
  Row,
  Container,
  Col,
  Card,
  Form,
  ListGroup,
  FormSelect,
} from 'react-bootstrap';
import { useParams } from 'react-router-dom';
// import { PassThrough } from 'stream';
import DefaultLayout from '../components/layouts/default-layout';
import ProductCard from '../components/product-card';
import Paginate from '../components/UI/paginate';
import { useAppDispatch, useAppSelector } from '../redux';
import { getFilterProducts } from '../redux/products/search-list';

const Products = () => {
  console.log('IN Products.tsx#######');
  const params = useParams();
  const { products, categories, subCategories} = useAppSelector(
  
    (state) => state.productFilter
  );

  const dispatch = useAppDispatch();
  const [category, setCategory] = useState<string>('');
  console.log('category:', category);
  const [subCategory, setSubCategory] = useState<string>('');
  console.log('subCategory:', subCategory);
  const [search, setSearch] = useState<string>('');
  console.log('search:', search);
  const keyword = params.keyword;

  const pageNumber = params.pageNumber || 1;

  const reset = () => {
    setCategory('');
    setSubCategory('');
    setSearch('');
  };

  useEffect(() => {
    console.log('Fetching data in useEffect');
    dispatch(
      getFilterProducts({ c: category, sc: subCategory, q: search})
    );
  }, [dispatch, pageNumber, category, subCategory, search]);

  return (
    <DefaultLayout>
      <Container>
        <Row>
          <Col lg={3}>
            <h2 className='py-4'>Filters</h2>
            <Card className='shadow p-3'>
              <ListGroup variant='flush'>
                <ListGroup.Item>
                  <h4 className='mb-2'>Super Category</h4>
                  <FormSelect
                    defaultValue={'All'}
                    onChange={(e: any) => {
                      if (e.target.value === 'All') {
                        reset();
                      } else {
                        setCategory(e.target.value);
                      }
                    }}
                  >
                    <option value='All'>All</option>
                    All
                    {categories.map((category: any) => (
                      <option value={category.cat_name} key={category.id}>
                        {category.cat_name}
                      </option>
                    ))}
                  </FormSelect>
                </ListGroup.Item>
                <ListGroup.Item>
                  <h4 className='mb-2'>Sub Category</h4>
                  <FormSelect
                    defaultValue={'All'}
                    onChange={(e: any) => {
                      if (e.target.value === 'All') {
                        reset();
                      } else {
                        // setBrand(e.target.value);
                        setSubCategory(e.target.value);

                      }
                    }}
                  >
                    <option value='All'>All</option>
                    All
                    {subCategories.map((subcategory: any) => (
                      <option value={subcategory.name} key={subcategory.id}>
                        {subcategory.name}
                      </option>
                    ))}
                  </FormSelect>
                </ListGroup.Item>
              </ListGroup>
            </Card>
          </Col>

          <Col lg={9}>
            <Row>
              <div className='col-md-6 pb-4'>
                <div className='d-flex'>
                  <Form.Control
                    onChange={(e: any) => setSearch(e.target.value)}
                    className='me-2'
                    placeholder='Search for product...'
                    value={search}
                  />
                </div>
              </div>
            </Row>
            <Row style={{ minHeight: '80vh' }}>
              {products.map((product) => (
                <Col lg={4} md={6} xs={12} key={product.id}>
                  <ProductCard product={product} />
                </Col>
              ))}
            </Row>
          </Col>
        </Row>
        <Paginate
          // pages={pages}
          // page={page}
          pages= {1}
          page= {1}
          keyword={keyword ? keyword : ''}
          isAdmin={false}
        />
      </Container>
    </DefaultLayout>
  );
};

export default Products;
