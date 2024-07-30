import PhotoSwipeLightbox from '../vendors/photoswipe/dist/photoswipe-lightbox.esm.min.js';
import PhotoSwipeDynamicCaption from '../vendors/photoswipe-dynamic-caption-plugin/photoswipe-dynamic-caption-plugin.esm.js';

const smallScreenPadding = {
  top: 0, bottom: 0, left: 0, right: 0
};
const largeScreenPadding = {
  top: 30, bottom: 30, left: 0, right: 0
};
const lightbox = new PhotoSwipeLightbox({
  gallerySelector: '.my-gallery',
  childSelector: '.pswp-gallery__item',
  
  // optionaly adjust viewport
  padding: { top: 100, bottom: 100, left: 100, right: 100 },
  pswpModule: () => import('../vendors/photoswipe/dist/photoswipe.esm.min.js')
});

const captionPlugin = new PhotoSwipeDynamicCaption(lightbox, {
  mobileLayoutBreakpoint: 1900,
  type: 'below',
  mobileCaptionOverlapRatio: 1
});

lightbox.init();