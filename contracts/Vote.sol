pragma solidity ^0.4.0;

contract Vote {
    struct Candidate {
        string name;
        uint votesCount;
    }

    struct Voter {
        bool voted;
    }

    address public owner;
    bool public closed;

    mapping(address => Voter) voters;
    Candidate[3] candidates;

    function Vote(string first, string second) public {
        owner = msg.sender;
        candidates[0] = Candidate({name: first, votesCount: 0});
        candidates[1] = Candidate({name: second, votesCount: 0});
        candidates[2] = Candidate({name: '', votesCount: 0}); // Against all candidate
    }

    function VoteFor(uint index) public {
        require(!closed);
        require(index < candidates.length - 1);
        Voter voter = voters[msg.sender];
        require(!voter.voted);
        candidates[index].votesCount++;
        voter.voted = true;
    }

    function GetResults() public constant returns(uint, uint, uint) {
        return (candidates[0].votesCount, candidates[1].votesCount, candidates[2].votesCount);
    }

    function Candidates() public constant returns(string, string) {
        return (candidates[0].name, candidates[1].name);
    }

    function Close() public {
        require(msg.sender == owner);
        closed = true;
    }

}
