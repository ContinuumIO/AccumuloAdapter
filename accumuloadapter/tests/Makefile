CC = gcc
CFLAGS = -g -Werror -Wall -Wdeclaration-after-statement
TEXT_INCLUDE_DIRS = -I ../textadapter -I ../lib

index.o: ../textadapter/index.c
	$(CC) $(CFLAGS) -c ../textadapter/index.c $(TEXT_INCLUDE_DIRS)

field_info.o: ../lib/field_info.c
	$(CC) $(CFLAGS) -c ../lib/field_info.c $(TEXT_INCLUDE_DIRS)

clean:
	-rm test_text_adapter
	-rm -f *.o

