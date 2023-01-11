package kr.hull.shop.service;


import kr.hull.shop.entity.Member;
import kr.hull.shop.repository.MemberRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import javax.transaction.Transactional;

@Service
// 개발할 때만 쓰는 것 개발하다가 에러나면 롤백해주는 주석이다.
@Transactional
@RequiredArgsConstructor //bean 주입방법 생성자 final member, @NonNull member 생성자 생성함
public class MemberService implements UserDetailsService {

    private final MemberRepository memberRepository;

    public Member saveMember(Member member){
        this.validateDuplicateMember(member);
        return memberRepository.save(member);
    }

    private void validateDuplicateMember(Member member){
        Member findMember = memberRepository.findByEmail(member.getEmail());
        if(findMember != null){
            throw new IllegalStateException("이미 가입된 회원입니다."); // 예외 처리
        }
    }

    @Override
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {

        Member member = memberRepository.findByEmail(email);

        if(member == null){
            throw new UsernameNotFoundException(email);
        }

        return User.builder()
                .username(member.getEmail())
                // 패스워드는 프론트단계에서 알 필요는 없음, 개인정보 유출이 될 수 있음
                // 백엔드에서는 암호화하여 처리해서 상대적으로 안전.
                .password(member.getPassword())
                .roles(member.getRole().toString())
                .build();
    }
}

