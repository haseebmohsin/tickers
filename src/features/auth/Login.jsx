import { useState } from 'react';
import LinkComponent from '../../components/LinkComponent';
import Button from '../../components/Button';
import AuthLayout from '../../components/layouts/AuthLayout';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    // const res = await loginUser({ email, password });

    // if (res.error) {
    //   setError('Invalid Credentials');
    // } else {
    //   Router.push(res.url);
    // }

    setIsLoading(false);
  };

  return (
    <>
      <section className='h-screen bg-gray-50 dark:bg-gray-900'>
        <div className='flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0'>
          <LinkComponent href='#' className='flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white'>
            Ticker
          </LinkComponent>

          <div className='w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700'>
            <div className='p-6 space-y-4 md:space-y-6 sm:p-8'>
              <h1 className='text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white'>
                Sign in to your account
              </h1>

              <form className='space-y-4 md:space-y-6'>
                <div>
                  <label htmlFor='email' className='block mb-2 text-sm font-medium text-gray-900 dark:text-white'>
                    Email
                  </label>
                  <input
                    type='email'
                    name='email'
                    id='email'
                    className='bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                    required=''
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>

                <div>
                  <label htmlFor='password' className='block mb-2 text-sm font-medium text-gray-900 dark:text-white'>
                    Password
                  </label>
                  <input
                    type='password'
                    name='password'
                    id='password'
                    className='bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                    required=''
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </div>

                <div className='flex items-center justify-between'>
                  <div className='flex items-start'>
                    <div className='flex items-center h-5'>
                      <input
                        id='remember'
                        aria-describedby='remember'
                        type='checkbox'
                        className='w-4 h-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded'
                      />
                    </div>
                    <label htmlFor='remember' className='ml-2 block text-sm font-medium text-gray-900 dark:text-white'>
                      Remember me
                    </label>
                  </div>
                  <div>
                    <LinkComponent
                      href='#'
                      className='text-sm font-medium text-primary-600 hover:text-primary-500 dark:hover:text-blue-500'>
                      Forgot your password?
                    </LinkComponent>
                  </div>
                </div>

                <div>
                  <Button className='w-full py-3' isLoading={isLoading} onClick={handleSubmit}>
                    Sign In
                  </Button>
                </div>
              </form>

              {error && <div className='flex text-lg text-red-600'>{error}</div>}
            </div>

            <div className='flex items-center justify-center p-4 bg-gray-100 dark:bg-gray-900 dark:border-gray-700'>
              <span className='text-sm font-medium text-gray-900 dark:text-white'>Don&apos;t have an account?</span>
              <LinkComponent
                href='/register'
                className='ml-2 text-sm font-medium text-primary-600 hover:text-primary-500 dark:hover:text-blue-500'>
                Sign Up
              </LinkComponent>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

Login.getLayout = function getLayout(page) {
  return <AuthLayout>{page}</AuthLayout>;
};

export default Login;
