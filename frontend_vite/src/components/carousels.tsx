import React from 'react';
import { useState } from 'react';
import { Carousel } from 'react-bootstrap';

const Carousels = () => {
  const [index, setIndex] = useState(0);

  const handleSelect = (selectedIndex: number) => {
    setIndex(selectedIndex);
  };

  return (
    <Carousel activeIndex={index} onSelect={handleSelect}>
      <Carousel.Item className='carsouel__item'>
        <img
          className='d-block w-full '
          // src='https://cdn.shopify.com/s/files/1/2301/4381/files/MSI_BANNER_1080x.jpg?v=1641895460'
          // src = 'https://i.insider.com/540f3701eab8eaf81065a627?width=700'
          src = '/imgs/iphone.jpg'
          alt='First slide'
        />
      </Carousel.Item>
      <Carousel.Item className='carsouel__item'>
        <img
          className='d-block w-full '
          src = 'https://c8.alamy.com/comp/2K2K5J1/robot-with-gift-boxes-isolated-contains-clipping-path-2K2K5J1.jpg'
          alt='Second slide'
        />
      </Carousel.Item>
      <Carousel.Item className='carsouel__item'>
        <img
          className='d-block w-full '
          src='https://m.media-amazon.com/images/I/71sXNOSFUlL._SL1100_.jpg'
          alt='Third slide'
        />
      </Carousel.Item>
    </Carousel>
  );
};

export default Carousels;
