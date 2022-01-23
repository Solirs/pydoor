package main

import(

	"fmt"
	"net"
	"log"

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
			buf := make([]byte, 4096)
			_, err := con.Read(buf)
			checkErr(err)
			fmt.Println("Server got:", string(buf))
	    }		
}




}