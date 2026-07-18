section .text
    global_start    ;entry point for linker

    _start:
        mov rax, 1  ; sys.write
        mov rdi, 1  ; stdout
        mov rsi, hello  ; message to write
        mov rdx, hello_len ; length of message
        syscall ; call kernel

        ; end program
        mov rax, 60 ; sys.exit
        mov rdi, 0  ; error code 0 (success)
        syscall     ; call kernel