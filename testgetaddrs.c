#include <sys/socket.h>
#include <sys/types.h>
//#include <linux/in.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <ifaddrs.h>
#include <stdio.h>
#include <stdint.h>


int main(void){
    struct ifaddrs *addrs,*tmp;

    getifaddrs(&addrs);
    tmp = addrs;

    while (tmp)
    {
        if (tmp->ifa_addr && tmp->ifa_addr->sa_family == AF_INET){
            struct sockaddr_in *test = NULL;
            char *addr = NULL;
            printf("%s\n", tmp->ifa_name);
            test = (struct sockaddr_in *) tmp->ifa_addr;
            
            addr = inet_ntoa(test->sin_addr);
            printf("%s\n", addr);
            
	}


        tmp = tmp->ifa_next;
    }

    freeifaddrs(addrs);
    return 0;
}
