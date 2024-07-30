// vanilla JS
// init with element
var grid = document.querySelector('.grid');
var msnry = new Masonry( grid, {
  // options...
  itemSelector: '.grid-item',
  columnWidth: 200
});
 
// init with selector
var msnry = new Masonry( '.grid', {
  // options...
});

import PhotoSwipeLightbox from '../vendors/photoswipe/dist/photoswipe-lightbox.esm.min.js';


const lightbox = new PhotoSwipeLightbox({
  gallery: '.masonry-gallery',
  children: 'a',
  pswpModule: () => import('../vendors/photoswipe/dist/photoswipe.esm.min.js'),
  loop: false,
  padding: { top: 20, bottom: 40, left: 100, right: 100 },
});

lightbox.init();