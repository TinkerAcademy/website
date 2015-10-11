/**
 * Calculates the 100th Fibonacci number. 
 * 
 * Fibonnaci sequence is the best approximation to estimate a rabbit population growth. 
 * 
 * The first 10 numbers of the sequence are 
 * F(0) = 0
 * F(1) = 1
 * F(2) = 1
 * F(3) = 2
 * F(4) = 3
 * F(5) = 5
 * F(6) = 8
 * F(7) = 13
 * F(8) = 21
 * F(9) = 34
 *   
 * The 11th number F(10) in the sequence would be 55 (34 + 21). 
 * The 12th number F(12) is 89 (55 + 34). 
 * 
 * In general, the nth number F(n) for n >= 2 can be found from F(n-2) and F(n-2) number
 * 
 * F(n) = F(n-1) + F(n-2)   
 * F(2) = F(0) + F(1)
 * F(3) = F(1) + F(2)
 * F(4) = F(2) + F(3)
 * ...  						
 * 
 */
package com.tinkeracademy.ap;

public class Main {

	public static void main(String[] args) {
		
		/* 
		 * (n-2)th number
		 * 
		 * Initialized to F(0)
		 *  
		 */
		int n_2 = 0;
		
		/* 
		 * (n-1)th number
		 * 
		 * Initialized to the second Fibonacci number F(1) = 1
		 *  
		 */
		int n_1 = 1;
		
		/* 
		 * nth number
		 * 
		 * Initialized to 0
		 *  
		 */
		int n = 0;
		
		/* 
		 * Why 23? Well, we have F(0) and F(1) and we need to calculate the next 23 Fibonacci numbers
		 */
		for (int i = 0; i < 23; i++) {
			
			// F(n) = F(n-1) + F(n-2)
			n = n_1 + n_2; 
			
			/* 
			 * TODO Add your code below
			 * 
			 * What should n_2 be updated to?
			 * What should n_1 be updated to?
			 */
		}
		
		System.out.println("n="+n);
	}

}
