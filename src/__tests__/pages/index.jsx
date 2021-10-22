import React from 'react';
import Index from 'animelister/src/pages/index';
import { mount } from 'enzyme';

it('renders homepage unchanged', () => {
  const tree = mount(<Index />);
  expect(tree).toMatchSnapshot();
});
