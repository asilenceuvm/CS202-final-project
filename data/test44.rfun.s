
  .globl id
id:
  pushq %rbp
  movq %rsp, %rbp
  subq $0, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14


  jmp id_start
id_start:
  movq %rdi, %rdx
  movq %rdx, %rdx
  movq %rdx, %rax
  jmp id_conclusion
id_conclusion:

  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq

  .globl f
f:
  pushq %rbp
  movq %rsp, %rbp
  subq $0, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14

  movq $0, (%r15)
  addq $8, %r15

  jmp f_start
label_1389:
  movq free_ptr(%rip), %rdx
  addq $24, free_ptr(%rip)
  movq %rdx, %r11
  movq $133, 0(%r11)
  movq %rdx, %r11
  movq %rbx, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -8(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %r12, %rdi
  movq %rdx, %rsi
  movq %r13, %rax
  
  addq $0, %rsp
  subq $8, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  jmp *%rax

label_1390:
  movq $0, %rdx
  jmp label_1389
label_1391:
  movq %r15, %rdi
  movq $24, %rsi
  callq collect
  jmp label_1389
label_1392:
  movq %rdx, %r11
  movq 8(%r11), %rcx
  movq %rdx, %r11
  movq 16(%r11), %rdx
  movq %rdx, %r11
  movq 8(%r11), %rdx
  movq %rdx, %rdi
  movq %rcx, %rax
  
  addq $0, %rsp
  subq $8, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  jmp *%rax

label_1393:
  leaq f(%rip), %r13
  movq %rcx, %r12
  addq $1, %r12
  movq %rdx, %r11
  movq 8(%r11), %rbx
  movq %rdx, %r11
  movq 16(%r11), %rax
  movq %rax, -8(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $24, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_1390
  jmp label_1391
f_start:
  movq %rdi, %rcx
  movq %rsi, %rdx
  cmpq $100, %rcx
  je label_1392
  jmp label_1393
f_conclusion:

  addq $0, %rsp
  subq $8, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq

  .globl main
main:
  pushq %rbp
  movq %rsp, %rbp
  subq $0, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14

  movq $16384, %rdi
  movq $16, %rsi
  callq initialize
  movq rootstack_begin(%rip), %r15
  movq $0, (%r15)
  addq $8, %r15

  jmp main_start
label_1394:
  movq free_ptr(%rip), %rdx
  addq $24, free_ptr(%rip)
  movq %rdx, %r11
  movq $133, 0(%r11)
  movq %rdx, %r11
  movq %rbx, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -8(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq $0, %rdi
  movq %rdx, %rsi
  movq %r12, %rax
  callq *%rax
  jmp main_conclusion
label_1395:
  movq $0, %rdx
  jmp label_1394
label_1396:
  movq %r15, %rdi
  movq $24, %rsi
  callq collect
  jmp label_1394
label_1397:
  movq free_ptr(%rip), %rdx
  addq $16, free_ptr(%rip)
  movq %rdx, %r11
  movq $3, 0(%r11)
  movq %rdx, %r11
  movq %r13, 8(%r11)
  movq $0, %rcx
  movq %rdx, -8(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $24, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_1395
  jmp label_1396
label_1398:
  movq $0, %rdx
  jmp label_1397
label_1399:
  movq %r15, %rdi
  movq $16, %rsi
  callq collect
  jmp label_1397
main_start:
  leaq f(%rip), %r12
  leaq id(%rip), %rbx
  movq $42, %r13
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $16, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_1398
  jmp label_1399
main_conclusion:

  movq %rax, %rdi
  callq print_int
  movq $0, %rax

  addq $0, %rsp
  subq $8, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq
