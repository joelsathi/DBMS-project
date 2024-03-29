import React from 'react';
import { Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { formatCurrency } from '../utils/helper';
import { ReviewTypes } from '../utils/interfaces';

export type Product = {
  sku: string; // sku for product variant
  id: number; // for product

  name: string;
  price: number;
  base_price: number;
  image_url: string;

  category: string; //super category
  subcategory: string;

  brand: string;
  description: string;

  discount_id: number;
  
  // needed?
  qty: number;
  createdAt: Date;
  reviews: ReviewTypes[];
};

type Props = {
  product: Product;
};

const ProductCard = ({ product }: Props) => {
  return (
    <Card className='my-3 p-3 rounded' style={{ height: '400px' }}>
      <Link to={`/products/${product.id}`}>
        <Card.Img
          src={product.image_url}
          variant='top'
          style={{ height: '300px', width: '100%', objectFit: 'contain' }}
        />
        <Card.Body>
          <Card.Title className='d-flex justify-content-between align-items-baseline mb-4'>
            <span className='fs-2'>{product.name}</span>
            <span className='ms-2 text-muted'>
              {formatCurrency(product.price | product.base_price)}
            </span>
          </Card.Title>
        </Card.Body>
      </Link>
    </Card>
  );
};

export default ProductCard;
