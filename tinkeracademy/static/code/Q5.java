package com.tinkeracademy.ap;

public class Q5 {

	  public static void main(String[] args) {		  
  		int x = -9;
  		int count = 0;
  		while (!(x == 0)) { 		            		
  		  if (x > 0) { 
  			 x = x - 1;            		
  		  } else if (x < 0) {		
  			 x = x + 2;            		
  		  } else {		
  			x = x - 2;            		
  		  } 	
  		  count++;
  		}		
  		System.out.println(count);

	  }
}
