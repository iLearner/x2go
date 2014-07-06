x2go
====
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
 #   P r o c e d u r e   f o r   I n s t a l l i n g   t h e   E D X   P l a t f o r m   o n   C u b i e t r u c k   U s i n g   a   B o o t i n g   S D   C a r d  
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
  
 O n   a   L i n u x   o r   U b u n t u   m a c h i n e   c o n n e c t e d   t o   t h e   I n t e r n e t   a n d   w h i c h   h a v e   a c c e s s  
 t o   a   S D   c a r d   S l o t   ( Y o u   c a n   a l s o   a c c e s s   a   S D   c a r d   t h r o u g h   a   U S B ) :  
  
 -   P u t   t h e   c o n t e n t s   o f   t h e   E D X   P l a t f o r m   I n s t a l l a t i o n   f i l e s   f o r   C u b i e t r u c k   o n   a n   e m p t y   f o l d e r .  
  
 -   C h a n g e   t h e   c u r r e n t   d i r e c t o r y   t o   t h i s   f o l d e r .  
  
 -   I n s e r t   a n   e m p t y   S D   c a r d   o n   t h e   c o r r e s p o n d i n g   s l o t .  
  
 -   R e p l a c i n g   $ { c a r d }   w i t h   t h e   S D   c a r d   d e v i c e   y o u   a r e   u s i n g   ( e g .   / d e v / s d c ,   p l e a s e   b e   s u r e   o f   t h i s  
     b e f o r e   p r o c e e d i n g ,   s o   n o t   d a m a g e   h a p p e n s ) ,   r u n :  
             p y t h o n   e x e c u t e   s d   $ { c a r d }  
  
 -   W h e n   f i n i s h e d ,   i t   w i l l   b e   s a f e   t o   t a k e   o u t   t h e   S D   c a r d ,   a n d   i t   w i l l   c o n t a i n   L u b u n t u   ( a s   s p e c i f i e d  
     o n   t h e   C u b i e t r u c k   w e b   s i t e )   a n d   t h e   E D X   i n s t a l l a t i o n   f i l e s   f o r   C u b i e t r u c k ,   I   c r e a t e d ,   o n   t h e  
     f o l d e r     " / h o m e / l i n a r o / E D X "  
  
 -   I n s e r t   t h e   c r e a t e d   S D   c a r d   o n   t h e   C u b i e t r u c k   S D   c a r d   s l o t ,   t u r n   o n   t h e   C u b i e t r u c k ,  
     a n d   L u b u n t u   w i l l   l o a d .  
  
 -   C h a n g e   d i r e c t o r y   a n d   r u n   t h e   f i r s t   p a r t   o f   t h e   s c r i p t   ( " u p d a t e "   f i l e ) .  
     N o t e :   T h e   i n i t i a l   i n s t a l l a t i o n   o f   L u b u n t u   o n   C u b i e t r u c k   h a s   P y t h o n 3  
             c d   / h o m e / l i n a r o / E D X  
             p y t h o n 3   e x e c u t e   u p d a t e  
  
 -   W h e n   f i n i s h e d   C u b i e t r u c k   w i l l   r e b o o t ,   s o   c h a n g e   d i r e c t o r y   a n d   r u n   t h e   s e c o n d   p a r t   o f   t h e   s c r i p t  
     w h i c h   c o n s i s t s   o f   t h e   E D X   i n s t a l l a t i o n   p r e v i o u s   s t e p s   ( " e d x P R E " )   a n d   t h e   m a i n   o n e   ( " e d x " ) .  
     Y o u   c a n   s e e   t h e   f i l e s   " e d x P R E "   a n d   " e d x "   f o r   b e t t e r   u n d e r s t a n d i n g .  
             c d   / h o m e / l i n a r o / E D X  
             p y t h o n 3   e x e c u t e   e d x P R E   e d x  
  
 -   A t   t h i s   p o i n t   t h e   i n s t a l l a t i o n   w i l l   f a i l   w h e n   r u n n i n g   " e d x " ,   t r y i n g   t o   m a k e   s u r e   N G I N X   i s   s t a r t e d .  
     A   r e b o o t   w i l l   f i x   t h i s ,   s o   r e b o o t   a n d   r e - r u n   " e d x " .  
             s u d o   r e b o o t  
             c d   / h o m e / l i n a r o / E D X  
             p y t h o n 3   e x e c u t e   e d x  
  
 -   A t   t h i s   p o i n t ,   o n e   m o r e   f a i l u r e   w i l l   h a p e n d   w h e n   t h e   i n s t a l l a t i o n   r u n s   " a p p a r m o r _ p a r s e r "   o n   t h e  
     " l o a d i n g   c o d e   s a n d b o x   p r o f i l e "   t a s k ,   b e c a u s e   o f   a n   i s s u e   w i t h   w a r n i n g s .   M y   f i x   f o r   t h i s   i s  
     e x p l a i n e d   i n   t h e   f i l e   " a p p a r m o r F I X "   w h i c h   h a s   t o   b e   r u n   n e x t .   Y o u   a l s o   h a v e   t o   r e - r u n   t h e  
     u n f i n i s h e d   " e d x " .  
             s u d o   r e b o o t  
             c d   / h o m e / l i n a r o / E D X  
             p y t h o n 3   e x e c u t e   a p p a r m o r F I X   e d x  
  
 -   A t   t h i s   p o i n t ,   t h e   E D X   I n s t a l l a t i o n   w i l l   c o m p l e t e   s u c c e s s f u l l y   h e r e ,   b u t   b e c a u s e   o f   c o n t i n o u s  
     d e v e l o p m e n t ,   n e w   i s s u e s   m a y   a p p e a r .   I n   t h i s   c a s e ,   t h e   o n l y   t h i n g   l e f t   t o   d o   i s   f o r   n o w :   r e b o o t i n g  
     a n d   t r y i n g   t o   r u n   " e d x "   a g a i n .   S i m i l a r l y ,   y o u   c a n   d o   t h i s   a f t e r   c a n c e l l i n g   t h e   r u n n i n g   o f   " e d x " ,   i f  
     i t   d e l a y s   t o o   l o n g   i n   a   s p e c i f i c   t a s k   ( w h i c h   n o r m a l y   r u n s   f a s t e r )   a s   i f   i t   a p p e a r s   t o   n e v e r   f i n i s h .  
     T h a t   h a p p e n e d   t o   m e   s o m e   t i m e s   a t   d i f f e r e n t   p o i n t s ,   m a y b e   b e c u a u s e   o f   a   b a d   i n t e r n e t   c o n n e c t i o n ,  
     n o t   t o o   s u r e .  
 