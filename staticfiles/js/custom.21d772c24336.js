
 

   window.onload = () => {
      ScrollReveal().reveal({reset: true });
      ScrollReveal().reveal('.scroll');
      ScrollReveal().reveal('.first-scroll', { duration: 600, delay: 200, easing:'ease-in-out', distance: '10px',origin: 'bottom'});
      ScrollReveal().reveal('.footer-scroll', { duration: 600,  easing:'ease-in-out', distance: '500px', origin: 'left'});

   };