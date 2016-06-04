#ifndef _TRY_CATCH
#define _TRY_CATCH

#include <stdio.h>
#include <setjmp.h>
/*Usage : 
 * #define EXEPTION1 (1)  //This is for the exceptions when you want to throw it
 * 
 *  TRY{
 *      printf("Do stuff\n");
 *      TROW( EXCEPTION1 );
 *  }
 *  CATCH ( EXCEPTION1 ){
 *      printf("Catch the exception your expecting\n");
 *  }
 *  ENDTRY;
 *
 *  Unsure how many systems these will work on. 
 */
#define TRY do { jmp_buf extend_buf__; switch( setjmp(extend_buf__) ) { case 0: while(1) {
#define CATCH(x) break; case x:
#define FINALLY break; } default: {
#define ENDTRY break; } } } while(0)
#define THROW(x) longjmp(extend_buf__, x)

#endif /*!_TRY_CATCH*/
