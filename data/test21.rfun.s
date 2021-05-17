
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
label_124:
  movq free_ptr(%rip), %rdx
  addq $16, free_ptr(%rip)
  movq %rdx, %r11
  movq $131, 0(%r11)
  movq %rdx, %r11
  movq -8(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq 8(%r11), %rdx
  movq %rdx, %r11
  movq 8(%r11), %rdx
  movq %rdx, %rax
  jmp main_conclusion
label_125:
  movq $0, %rdx
  jmp label_124
label_126:
  movq %r15, %rdi
  movq $16, %rsi
  callq collect
  jmp label_124
label_127:
  movq free_ptr(%rip), %rdx
  addq $16, free_ptr(%rip)
  movq %rdx, %r11
  movq $3, 0(%r11)
  movq %rdx, %r11
  movq %rbx, 8(%r11)
  movq $0, %rcx
  movq %rdx, -8(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $16, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_125
  jmp label_126
label_128:
  movq $0, %rdx
  jmp label_127
label_129:
  movq %r15, %rdi
  movq $16, %rsi
  callq collect
  jmp label_127
main_start:
  movq $42, %rbx
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $16, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_128
  jmp label_129
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
