package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net"
)


func checkErr(err error){
	if err != nil{
		log.Fatal(err)
	}
}



func main(){

	lis, err := net.Listen("tcp", ":35891")

	checkErr(err)





	

	for {


		con, err := lis.Accept()
		

		checkErr(err)
	
		for {
			data, err := ioutil.ReadAll(con)
			checkErr(err)
			fmt.Println("Server got:", string(data))
	    }		
}




}