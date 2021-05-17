
  .globl map
map:
  pushq %rbp
  movq %rsp, %rbp
  subq $0, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14

  movq $0, (%r15)
  addq $8, %r15

  jmp map_start
label_1318:
  movq free_ptr(%rip), %rdx
  addq $24, free_ptr(%rip)
  movq %rdx, %r11
  movq $5, 0(%r11)
  movq %rdx, %r11
  movq %r12, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 16(%r11)
  movq $0, %rcx
  movq %rdx, %rdx
  movq %rdx, %rax
  jmp map_conclusion
label_1319:
  movq $0, %rdx
  jmp label_1318
label_1320:
  movq %r15, %rdi
  movq $24, %rsi
  callq collect
  jmp label_1318
map_start:
  movq %rdi, %rbx
  movq %rsi, -8(%r15)
  movq -8(%r15), %r11
  movq 8(%r11), %rdx
  movq %rdx, %rdi
  movq %rbx, %rax
  callq *%rax
  movq %rax, %r12
  movq -8(%r15), %r11
  movq 16(%r11), %rdx
  movq %rdx, %rdi
  movq %rbx, %rax
  callq *%rax
  movq %rax, %rbx
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $24, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_1319
  jmp label_1320
map_conclusion:

  addq $0, %rsp
  subq $8, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq

  .globl add1
add1:
  pushq %rbp
  movq %rsp, %rbp
  subq $0, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14


  jmp add1_start
add1_start:
  movq %rdi, %rdx
  movq %rdx, %rdx
  addq $1, %rdx
  movq %rdx, %rax
  jmp add1_conclusion
add1_conclusion:

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
label_1321:
  movq free_ptr(%rip), %rdx
  addq $24, free_ptr(%rip)
  movq %rdx, %r11
  movq $5, 0(%r11)
  movq %rdx, %r11
  movq %r13, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r12, 16(%r11)
  movq $0, %rcx
  leaq map(%rip), %rcx
  movq %rbx, %rdi
  movq %rdx, %rsi
  movq %rcx, %rax
  callq *%rax
  movq %rax, %rdx
  movq %rdx, %r11
  movq 16(%r11), %rdx
  movq %rdx, %rax
  jmp main_conclusion
label_1322:
  movq $0, %rdx
  jmp label_1321
label_1323:
  movq %r15, %rdi
  movq $24, %rsi
  callq collect
  jmp label_1321
main_start:
  leaq add1(%rip), %rbx
  movq $0, %r13
  movq $41, %r12
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $24, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_1322
  jmp label_1323
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
