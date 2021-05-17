
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


  jmp f_start
f_start:
  movq %rdi, %rcx
  movq %rcx, %r11
  movq 8(%r11), %rdx
  movq %rcx, %r11
  movq 16(%r11), %rcx
  movq %rcx, %r11
  movq 8(%r11), %rcx
  movq %rcx, %rdi
  movq %rdx, %rax
  
  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  jmp *%rax

f_conclusion:

  addq $0, %rsp
  subq $0, %r15
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
label_1468:
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
  movq %rdx, %rdi
  movq %r12, %rax
  callq *%rax
  jmp main_conclusion
label_1469:
  movq $0, %rdx
  jmp label_1468
label_1470:
  movq %r15, %rdi
  movq $24, %rsi
  callq collect
  jmp label_1468
label_1471:
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
  jl label_1469
  jmp label_1470
label_1472:
  movq $0, %rdx
  jmp label_1471
label_1473:
  movq %r15, %rdi
  movq $16, %rsi
  callq collect
  jmp label_1471
main_start:
  leaq f(%rip), %r12
  leaq id(%rip), %rbx
  movq $42, %r13
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $16, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_1472
  jmp label_1473
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
