
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
label_1346:
  movq free_ptr(%rip), %rdx
  addq $16, free_ptr(%rip)
  movq %rdx, %r11
  movq $3, 0(%r11)
  movq %rdx, %r11
  movq %rbx, 8(%r11)
  movq $0, %rcx
  movq %r12, %rdi
  movq %rdx, %rsi
  movq %r13, %rax
  
  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  jmp *%rax

label_1347:
  movq $0, %rdx
  jmp label_1346
label_1348:
  movq %r15, %rdi
  movq $16, %rsi
  callq collect
  jmp label_1346
label_1349:
  movq %rdx, %r11
  movq 8(%r11), %rdx
  movq %rdx, %rax
  jmp f_conclusion
label_1350:
  leaq f(%rip), %r13
  movq %rcx, %r12
  addq $1, %r12
  movq %rdx, %r11
  movq 8(%r11), %rbx
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $16, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_1347
  jmp label_1348
f_start:
  movq %rdi, %rcx
  movq %rsi, %rdx
  cmpq $100, %rcx
  je label_1349
  jmp label_1350
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

  jmp main_start
label_1351:
  movq free_ptr(%rip), %rdx
  addq $16, free_ptr(%rip)
  movq %rdx, %r11
  movq $3, 0(%r11)
  movq %rdx, %r11
  movq %rbx, 8(%r11)
  movq $0, %rcx
  movq $0, %rdi
  movq %rdx, %rsi
  movq %r12, %rax
  callq *%rax
  jmp main_conclusion
label_1352:
  movq $0, %rdx
  jmp label_1351
label_1353:
  movq %r15, %rdi
  movq $16, %rsi
  callq collect
  jmp label_1351
main_start:
  leaq f(%rip), %r12
  movq $42, %rbx
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $16, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_1352
  jmp label_1353
main_conclusion:

  movq %rax, %rdi
  callq print_int
  movq $0, %rax

  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq
