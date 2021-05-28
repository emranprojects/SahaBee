import { render, screen } from '@testing-library/react';
import Login from './Login';

test('renders login form', () => {
  render(<Login />);
  const buttonElement = screen.getByText(/login/i);
  const usernameElement = screen.getByText(/user/i);
  const passwordElement = screen.getByText(/pass/i);
  expect(buttonElement).toBeInTheDocument();
  expect(usernameElement).toBeInTheDocument();
  expect(passwordElement).toBeInTheDocument();
});
