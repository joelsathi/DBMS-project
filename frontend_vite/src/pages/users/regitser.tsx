import React from 'react';
import FormContainer from '../../components/UI/form-container';
import { Button, Form } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as Yup from 'yup';
import publicAxios from '../../utils/public-axios';
import toast from 'react-hot-toast';
import { setError } from '../../utils/error';

type FormValues = {
  name: string;
  firstname: string;
  lastname: string;
  email: string;
  address: String;
  password: string;
  confirmPassword: string;
  cardnumber: string;
  provider: string;
  mobilenumber: string;
};

const Register = () => {
  const navigate = useNavigate();
  const phoneRegExp = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
  const validationSchema = Yup.object().shape({
    name: Yup.string()
      .required('Username is required')
      .min(6, 'Username must be at least 6 characters')
      .max(20, 'Username must not exceed 20 characters'),
    firstname: Yup.string()
      .required("First name is required"),
    lastname: Yup.string()
      .required("Last name is required"),
    email: Yup.string().required('Email is required').email('Email is invalid'),
    password: Yup.string()
      .required('Password is required')
      .min(6, 'Password must be at least 6 characters')
      .max(40, 'Password must not exceed 40 characters'),
    address: Yup.string()
      .required("Address is required"),
    cardNumber: Yup.string()
      .required('Card number is required')
      .matches(/^(?:4[0-9]{12}(?:[0-9]{3})?|(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})$/, 'Invalid card number format'),
    // expDate: Yup.string()
    //   .required('Expiration date is required').matches(/^(0[1-9]|1[0-2])\/[0-9]{2}$/, 'Invalid expiration date format'),
    // cvv: Yup.string()
    //   .required('CVV is required')
    //   .matches(/^[0-9]{3,4}$/, 'Invalid CVV format'),
    provider: Yup.string()
      .required('Provider is required')
      .oneOf(['Visa', 'MasterCard', 'American Express', 'Discover'], 'Invalid provider'),
    confirmPassword: Yup.string()
      .required('Confirm Password is required')
      .oneOf([Yup.ref('password'), null], 'Confirm Password does not match'),
    phoneNumber: Yup.string()
      .matches(phoneRegExp, 'Phone number is not valid')
      .required('Phone number is required')
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: yupResolver(validationSchema),
  });

  const onSubmit = (data: FormValues) => {
    publicAxios
      .post('/users/register', data)
      .then((res) => {
        toast.success('you have been registred , please login');
        navigate('/login');
      })
      .catch((err) => toast.error(setError(err)));
  };

  return (
    <FormContainer
      meta='register for free'
      image='https://blog.hubspot.com/hubfs/ecommerce-1.png'
      title='Create account'
    >
      <Form onSubmit={handleSubmit(onSubmit)}>
        <Form.Group controlId='name'>
          <Form.Label>Username</Form.Label>
          <Form.Control
            placeholder='Enter name'
            {...register('name')}
            className={errors.name?.message && 'is-invalid'}
          />
          <p className='invalid-feedback'>{errors.name?.message}</p>
        </Form.Group>

        <Form.Group controlId='name'>
          <Form.Label>First name</Form.Label>
          <Form.Control
            placeholder='Enter first name'
            {...register('firstname')}
            className={errors.firstname?.message && 'is-invalid'}
          />
          <p className='invalid-feedback'>{errors.firstname?.message}</p>
        </Form.Group>

        <Form.Group controlId='name'>
          <Form.Label>Last name</Form.Label>
          <Form.Control
            placeholder='Enter last name'
            {...register('lastname')}
            className={errors.lastname?.message && 'is-invalid'}
          />
          <p className='invalid-feedback'>{errors.lastname?.message}</p>
        </Form.Group>

        <Form.Group controlId='email'>
          <Form.Label>Email</Form.Label>

          <Form.Control
            type='email'
            placeholder='Enter email'
            {...register('email')}
            className={errors.email?.message && 'is-invalid'}
          />
          <p className='invalid-feedback'>{errors.email?.message}</p>
        </Form.Group>

        <Form.Group controlId='address'>
          <Form.Label>Address</Form.Label>

          <Form.Control
            type='email'
            placeholder='Enter address'
            {...register('address')}
            className={errors.address?.message && 'is-invalid'}
          />
          <p className='invalid-feedback'>{errors.address?.message}</p>
        </Form.Group>

        <Form.Group controlId='mobilenumber'>
          <Form.Label>Mobile Number</Form.Label>

          <Form.Control
            type='email'
            placeholder='Enter mobile number'
            {...register('address')}
            className={errors.mobilenumber?.message && 'is-invalid'}
          />
          <p className='invalid-feedback'>{errors.mobilenumber?.message}</p>
        </Form.Group>

        <Form.Group controlId='password'>
          <Form.Label>Password </Form.Label>

          <Form.Control
            type='password'
            placeholder='*******'
            {...register('password')}
            className={errors.password?.message && 'is-invalid'}
          />
          <p className='invalid-feedback'>{errors.password?.message}</p>
        </Form.Group>

        <Form.Group controlId='confirmPassword'>
          <Form.Label>Confirm Password </Form.Label>

      
        <Form.Group controlId='confirmPassword'></Form.Group>

          <Form.Control
            type='password'
            placeholder='*******'
            {...register('confirmPassword')}
            className={errors.confirmPassword?.message && 'is-invalid'}
          />
          <p className='invalid-feedback'>{errors.confirmPassword?.message}</p>
          
          <br/>
        <p>Payment options</p>
    
        </Form.Group>

        <Form.Group controlId='cardnumer'>
          <Form.Label>Card Number </Form.Label>

          <Form.Control
            type='cardnumber'
            placeholder='Enter card number'
            {...register('cardnumber')}
            className={errors.cardnumber?.message && 'is-invalid'}
          />
          <p className='invalid-feedback'>{errors.cardnumber?.message}</p>
        </Form.Group>

        <Form.Group controlId='provider'>
          <Form.Label>Provider </Form.Label>

          <Form.Control
            type='provider'
            placeholder='Enter provider'
            {...register('provider')}
            className={errors.provider?.message && 'is-invalid'}
          />
          <p className='invalid-feedback'>{errors.provider?.message}</p>
        </Form.Group>

          <Link to='/login' className='float-end me-2 mt-1'>
            Already have an Account ? Login
          </Link>
        

        <Button
          style={{ backgroundColor: '#e03a3c', color: '#fff' }}
          variant='outline-none'
          type='submit'
          className='mt-4 w-full'
        >
          Register
        </Button>
      </Form>
    </FormContainer>
  );
};

export default Register;
